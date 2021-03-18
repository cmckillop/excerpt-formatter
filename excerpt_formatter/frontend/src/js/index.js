import 'css/main.scss';
import {dom, library} from '@fortawesome/fontawesome-svg-core'
import {
    faBackspace,
    faCalendarAlt,
    faCheckCircle,
    faClock,
    faIndent,
    faInfoCircle,
    faKey,
    faListOl,
    faPaperPlane,
    faShare,
    faSortNumericUp,
    faTimesCircle,
    faUserClock
} from '@fortawesome/free-solid-svg-icons'
import {faSlackHash} from '@fortawesome/free-brands-svg-icons'

library.add(
    faPaperPlane,
    faBackspace,
    faClock,
    faCalendarAlt,
    faCheckCircle,
    faIndent,
    faInfoCircle,
    faTimesCircle,
    faKey,
    faListOl,
    faShare,
    faSlackHash,
    faUserClock,
    faSortNumericUp)
dom.watch()


const FORMAT_PATH = '/format'
const MESSAGE_PATH = '/slack/message'
const AUTHENTICATION_PATH = '/slack/authenticate'
const CHANNEL_PATH = '/slack/channel'

async function getAuthenticationRequest() {
    const auth_token = document.getElementById('input-auth-token').value
    const response = await fetch(AUTHENTICATION_PATH, {
        method: 'GET',
        headers: {
            'auth-token': auth_token
        }
    });
    return response.json();
}

async function getChannelName() {
    const auth_token = document.getElementById('input-auth-token').dataset.token;
    const url = `${CHANNEL_PATH}/${document.getElementById('input-channel-id').value}`
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'auth-token': auth_token
        }
    });
    return response.json();
}

async function postMessageRequest() {
    const postData = {
        'slack_api_key': document.getElementById('input-auth-token').dataset.token,
        'channel_id': document.getElementById('input-channel-id').dataset.channelId,
        'excerpt_number': document.getElementById('input-excerpt-number').value,
        'text': document.getElementById('textarea-message').value,
        'word_count': parseInt(document.getElementById('tag-word-count').dataset.wordCount)
    };

    const response = await fetch(MESSAGE_PATH, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    });
    return response.json();
}

async function postFormatRequest() {

    let postData;

    const offsetTime = document.getElementById('input-offset-time').value;
    if (offsetTime === '') {
        postData = {
            'preserve_paragraphs': document.getElementById('select-paragraphs').value,
            'segment_count': document.getElementById('input-excerpt-counter').value,
            'text': document.getElementById('textarea-format').value
        };
    } else {
        postData = {
            'offset_time': document.getElementById('input-offset-time').value,
            'preserve_paragraphs': document.getElementById('select-paragraphs').value,
            'segment_count': document.getElementById('input-excerpt-counter').value,
            'text': document.getElementById('textarea-format').value
        };
    }

    console.log(JSON.stringify(postData));

    const response = await fetch(FORMAT_PATH, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
    });
    return response.json();
}

document.getElementById('button-format-text').addEventListener('click', function () {
    postFormatRequest().then(data => {
        document.getElementById('textarea-message').value = data['formatted_text'];
        document.getElementById('input-excerpt-number').value = data['excerpt_number'];
        const wordCount = data['word_count'];
        document.getElementById('tag-word-count').innerText = `${wordCount} Words`;
        document.getElementById('tag-word-count').dataset.wordCount = wordCount;
    });
});

document.getElementById('button-send-message').addEventListener('click', function () {
    postMessageRequest();
});

document.getElementById('button-clear-offset-time').addEventListener('click', function () {
    document.getElementById('input-offset-time').value = '';
});

document.getElementById('button-auth-token').addEventListener('click', function () {
    getAuthenticationRequest().then(data => {
        const inputAuthToken = document.getElementById('input-auth-token');
        const authTokenStatusIcon = document.getElementById('auth-token-status-icon');
        if (data['ok']) {
            inputAuthToken.dataset.token = inputAuthToken.value;
            inputAuthToken.value = data['team'];
            inputAuthToken.classList.add('has-text-success');
            inputAuthToken.classList.add('is-primary');
            authTokenStatusIcon.classList.add('has-text-success');
            authTokenStatusIcon.firstElementChild.classList.replace(
                'fa-info-circle', 'fa-check-circle');
            inputAuthToken.toggleAttribute('readonly');
            document.getElementById('button-auth-token').toggleAttribute('disabled');
            document.getElementById('button-auth-token').classList.add('is-success');
        } else {
            inputAuthToken.classList.add('has-text-danger');
            inputAuthToken.classList.add('is-danger');
            authTokenStatusIcon.classList.add('has-text-danger');
            authTokenStatusIcon.firstElementChild.classList.replace(
                'fa-info-circle', 'fa-times-circle');
            document.getElementById('button-auth-token').classList.add('is-danger');
        }
    });
});

document.getElementById('button-channel-id').addEventListener('click', function () {
    const inputChannelId = document.getElementById('input-channel-id');
    const channelIdStatusIcon = document.getElementById('channel-id-status-icon');
    getChannelName().then(data => {
        console.log(data);
        if (data['ok']) {
            inputChannelId.dataset.channelId = inputChannelId.value;
            inputChannelId.value = data['name'];
            inputChannelId.classList.add('has-text-success');
            inputChannelId.classList.add('is-primary');
            channelIdStatusIcon.classList.add('has-text-success');
            channelIdStatusIcon.firstElementChild.classList.replace(
                'fa-info-circle', 'fa-check-circle');
            inputChannelId.toggleAttribute('readonly');
            document.getElementById('button-channel-id').toggleAttribute('disabled');
            document.getElementById('button-channel-id').classList.add('is-success');
        } else {
            inputChannelId.classList.add('has-text-danger');
            inputChannelId.classList.add('is-danger');
            channelIdStatusIcon.classList.add('has-text-danger');
            channelIdStatusIcon.firstElementChild.classList.replace(
                'fa-info-circle', 'fa-times-circle');
            document.getElementById('button-channel-id').classList.add('is-danger');
        }
    });
});