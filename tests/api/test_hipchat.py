''' Tests for boss.api.hipchat module. '''

from pytest import fixture
from mock import patch
from boss.api import hipchat
from boss.core.constants.notification_types import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED,
    RUNNING_SCRIPT_STARTED,
    RUNNING_SCRIPT_FINISHED
)


@fixture(scope='function')
def base_url():
    return hipchat.API_BASE_URL.format(
        company_name=hipchat.config()['company_name'],
        room_id=hipchat.config()['room_id'],
        auth_token=hipchat.config()['auth_token']
    )


def test_create_link():
    ''' Test hipchat.create_link(). '''
    url = 'http://test-link-url'
    title = 'Test link'
    expected_link = '<a href="{url}">{title}</a>'.format(url=url, title=title)

    assert hipchat.create_link(url, title) == expected_link


def test_notity_deploying(base_url):
    ''' Test hipchat.notify_deploying(). '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='temp',
        commit='tttt',
        commit_url='http://commit-url',
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        user='user',
    )
    payload = {
        'color': 'green',
        'message': 'user is deploying <a href="http://repository-url">project-name</a>:<a href="http://branch-url">temp</a> (<a href="http://commit-url">tttt</a>) to <a href="http://public-url">stage</a> server.',
        'notify': True,
        'message_format': 'html'
    }

    with patch('requests.post') as mock_post:
        hipchat.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deployed(base_url):
    ''' Test hipchat.notify_deployed(). '''
    notify_params = dict(
        branch_url='http://branch-url',
        branch='temp',
        commit='tttt',
        commit_url='http://commit-url',
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        user='user',
    )
    payload = {
        'color': 'purple',
        'message': 'user finished deploying <a href="http://repository-url">project-name</a>:<a href="http://branch-url">temp</a> (<a href="http://commit-url">tttt</a>) to <a href="http://public-url">stage</a> server.',
        'notify': True,
        'message_format': 'html'
    }

    with patch('requests.post') as mock_post:
        hipchat.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deploying_with_no_branch(base_url):
    '''
    Test hipchat.notify_deploying() doesn't show branch link,
    if branch is not provided.
    '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        commit='tttt',
        commit_url='http://commit-url',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        user='user',
    )
    payload = {
        'color': 'green',
        'message': 'user is deploying <a href="http://repository-url">project-name</a> (<a href="http://commit-url">tttt</a>) to <a href="http://public-url">stage</a> server.',
        'notify': True,
        'message_format': 'html'
    }

    with patch('requests.post') as mock_post:
        hipchat.send(DEPLOYMENT_STARTED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_notity_deployed_with_no_branch(base_url):
    '''
    Test hipchat.notify_deployed() doesn't show branch link,
    if branch is not provided.
    '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        commit='tttt',
        commit_url='http://commit-url',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        user='user',
    )
    payload = {
        'color': 'purple',
        'message': 'user finished deploying <a href="http://repository-url">project-name</a> (<a href="http://commit-url">tttt</a>) to <a href="http://public-url">stage</a> server.',
        'notify': True,
        'message_format': 'html'
    }

    with patch('requests.post') as mock_post:
        hipchat.send(DEPLOYMENT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_send_running_script_started_notification(base_url):
    ''' Test send() sends RUNNING_SCRIPT_STARTED notfication. '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        script='migration',
        user='user'
    )

    payload = {
        'color': 'green',
        'notify': True,
        'message_format': 'html',
        'message': 'user is running migration for <a href="http://repository-url">project-name</a> on <a href="http://public-url">stage</a> server.'
    }

    with patch('requests.post') as mock_post:
        hipchat.send(RUNNING_SCRIPT_STARTED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)


def test_send_running_script_finished_notification(base_url):
    ''' Test send() sends RUNNING_SCRIPT_FINISHED notfication. '''
    notify_params = dict(
        public_url='http://public-url',
        host='test-notify-deploying-host',
        repository_url='http://repository-url',
        project_name='project-name',
        server_name='stage',
        server_link='http://server-link',
        script='migration',
        user='user'
    )

    payload = {
        'color': 'purple',
        'notify': True,
        'message_format': 'html',
        'message': 'user finished running migration for <a href="http://repository-url">project-name</a> on <a href="http://public-url">stage</a> server.'
    }

    with patch('requests.post') as mock_post:
        hipchat.send(RUNNING_SCRIPT_FINISHED, **notify_params)
        mock_post.assert_called_once_with(base_url, json=payload)
