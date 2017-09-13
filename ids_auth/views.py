from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from .models import AgaveOAuthToken
import logging
import os
import requests
import time

logger = logging.getLogger(__name__)


def login_prompt(request):
    return render(request, 'ids_auth/login.html')


def agave_oauth(request):
    tenant_base_url = getattr(settings, 'AGAVE_TENANT_BASEURL')
    client_key = getattr(settings, 'AGAVE_CLIENT_KEY')

    logger.info("tenant url: %s, system consumer key: %s" % (tenant_base_url, client_key))

    session = request.session
    session['auth_state'] = os.urandom(24).encode('hex')
    next_page = request.GET.get('next')
    if next_page:
        session['next'] = next_page

    redirect_uri = reverse('ids_auth:agave_oauth_callback')

    authorization_url = (
        '%s/authorize?client_id=%s&response_type=code&redirect_uri=%s&state=%s' % (
            tenant_base_url,
            client_key,
            request.build_absolute_uri(redirect_uri),
            session['auth_state'],
        )
    )
    return HttpResponseRedirect(authorization_url)


def agave_oauth_callback(request):
    state = request.GET.get('state')

    if request.session['auth_state'] != state:
        msg = ('OAuth Authorization State mismatch!? auth_state=%s '
               'does not match returned state=%s' % (request.session['auth_state'], state))
        logger.error(msg)
        return HttpResponseBadRequest('Authorization State Failed')

    # logger.debug('callback, request.GET: %s' % request.GET)

    if 'code' in request.GET:
        # obtain a token for the user
        code = request.GET['code']
        tenant_base_url = getattr(settings, 'AGAVE_TENANT_BASEURL')
        client_key = getattr(settings, 'AGAVE_CLIENT_KEY')
        client_sec = getattr(settings, 'AGAVE_CLIENT_SECRET')
        redirect_uri = request.build_absolute_uri(
            reverse('ids_auth:agave_oauth_callback'))


	logger.debug('callback, redirect uri: %s' % redirect_uri)

        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }

	logger.debug('post request body: %s' % body)

        response = requests.post('%s/token' % tenant_base_url,
                                 data=body,
                                 auth=(client_key, client_sec))
        token_data = response.json()
        token_data['created'] = int(time.time())


	logger.debug('token_data: %s' % token_data)

        # log user in
        user = authenticate(backend='agave', token=token_data['access_token'])

	logger.debug('user: %s' % user)

        if user:

            try:
                token = user.agave_oauth
                token.update(**token_data)
            except ObjectDoesNotExist:
                token = AgaveOAuthToken(**token_data)
                token.user = user

            token.save()

            request.session[getattr(settings, 'AGAVE_TOKEN_SESSION_ID')] = token.token

            login(request, user)
            messages.success(request, 'Login successful. Welcome back, %s %s!' %
                (user.first_name, user.last_name))
        else:
            messages.warning(
                request,
                'Authentication failed. Please try again. If this problem '
                'persists please submit a support ticket.'
            )
            return HttpResponseRedirect(reverse('ids_auth:login'))
    else:
        if 'error' in request.GET:
            error = request.GET['error']
            logger.error('Authorization failed: %s' % error)

        messages.warning(request, 'Authentication failed.  Did you forget your password?'
                        '<ahref="https://user.iplantcollaborative.org/reset/request"Click here</a>'
                        'to reset your password.')
        return HttpResponseRedirect(reverse('ids_auth:login'))

    if 'next' in request.session:
        next_uri = request.session.pop('next')
        return HttpResponseRedirect(next_uri)
    else:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

