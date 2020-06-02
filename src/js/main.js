import 'css/main.scss';
import {dom, library} from '@fortawesome/fontawesome-svg-core'
import {faClock, faKey, faLightbulb, faPaperPlane, faTimesCircle} from '@fortawesome/free-solid-svg-icons'
import {faSlackHash} from '@fortawesome/free-brands-svg-icons'

library.add(faPaperPlane, faClock, faTimesCircle, faKey, faLightbulb, faSlackHash)
dom.watch()


const FORMAT_PATH = '/format'
const MESSAGE_PATH = '/message'

async function postMessageRequest() {
    const postData = {
        'slack_api_key': document.getElementById('input-api-token').value,
        'channel_id': document.getElementById('input-channel-id').value,
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

    const dateTime = document.getElementById('input-date-time').value;
    if (dateTime === '') {
        postData = {
            'preserve_paragraphs': document.getElementById('select-paragraphs').value,
            'text': document.getElementById('textarea-format').value
        };
    } else {
        postData = {
            'date_time': document.getElementById('input-date-time').value,
            'preserve_paragraphs': document.getElementById('select-paragraphs').value,
            'text': document.getElementById('textarea-format').value
        };
    }

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

document.getElementById('button-clear-date-time').addEventListener('click', function () {
    document.getElementById('input-date-time').value = '';
});