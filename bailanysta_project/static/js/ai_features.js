/**
 * JavaScript for AI content generation and hashtag search features
 */

document.addEventListener('DOMContentLoaded', function() {
    // AI Content Generation
    const aiGenerateBtn = document.getElementById('ai-generate-btn');
    const aiPromptInput = document.getElementById('ai-prompt-input');
    const postContentTextarea = document.getElementById('postContent');
    
    if (aiGenerateBtn && aiPromptInput && postContentTextarea) {
        aiGenerateBtn.addEventListener('click', function() {
            const prompt = aiPromptInput.value.trim();
            if (!prompt) {
                alert('Please enter a prompt for AI content generation');
                return;
            }
            
            // Show loading state
            aiGenerateBtn.disabled = true;
            aiGenerateBtn.textContent = 'Generating...';
            
            // Call the AI content generation API
            fetch('/ai/generate-content/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    prompt: prompt,
                    max_length: 280
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.content) {
                    postContentTextarea.value = data.content;
                    
                    // Optionally suggest hashtags for the generated content
                    suggestHashtags(data.content);
                } else if (data.error) {
                    alert('Error: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error generating content. Please try again.');
            })
            .finally(() => {
                // Reset button state
                aiGenerateBtn.disabled = false;
                aiGenerateBtn.textContent = 'Generate with AI';
            });
        });
    }
    
    // Hashtag Suggestion
    const suggestHashtagsBtn = document.getElementById('suggest-hashtags-btn');
    const hashtagContainer = document.getElementById('hashtag-suggestions');
    
    if (suggestHashtagsBtn && postContentTextarea && hashtagContainer) {
        suggestHashtagsBtn.addEventListener('click', function() {
            const content = postContentTextarea.value.trim();
            if (!content) {
                alert('Please enter some content first');
                return;
            }
            
            suggestHashtags(content);
        });
    }
    
    function suggestHashtags(content) {
        // Show loading state
        if (suggestHashtagsBtn) {
            suggestHashtagsBtn.disabled = true;
            suggestHashtagsBtn.textContent = 'Suggesting...';
        }
        
        // Call the hashtag suggestion API
        fetch('/ai/suggest-hashtags/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                content: content,
                max_hashtags: 5
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.hashtags && data.hashtags.length > 0) {
                // Display suggested hashtags
                hashtagContainer.innerHTML = '';
                data.hashtags.forEach(hashtag => {
                    const tag = document.createElement('span');
                    tag.className = 'badge bg-primary me-2 mb-2';
                    tag.textContent = hashtag;
                    tag.style.cursor = 'pointer';
                    
                    // Add click event to add hashtag to post content
                    tag.addEventListener('click', function() {
                        postContentTextarea.value = postContentTextarea.value.trim() + ' ' + hashtag;
                    });
                    
                    hashtagContainer.appendChild(tag);
                });
                
                // Show the container
                hashtagContainer.style.display = 'block';
            } else {
                hashtagContainer.innerHTML = '<p class="text-muted">No hashtag suggestions available</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            hashtagContainer.innerHTML = '<p class="text-danger">Error suggesting hashtags</p>';
        })
        .finally(() => {
            // Reset button state
            if (suggestHashtagsBtn) {
                suggestHashtagsBtn.disabled = false;
                suggestHashtagsBtn.textContent = 'Suggest Hashtags';
            }
        });
    }
    
    // Hashtag Search
    const hashtagSearchForm = document.getElementById('hashtag-search-form');
    const hashtagSearchInput = document.getElementById('hashtag-search-input');
    const searchResultsContainer = document.getElementById('search-results');
    
    if (hashtagSearchForm && hashtagSearchInput) {
        hashtagSearchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const hashtag = hashtagSearchInput.value.trim();
            if (!hashtag) {
                return;
            }
            
            // Search for posts with the hashtag - use window.location to get HTML response
            window.location.href = '/posts/?hashtag=' + encodeURIComponent(hashtag.replace('#', ''));
        });
    }
    
    // Utility function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Handle clickable hashtags in post content
    document.querySelectorAll('.post-content').forEach(function(element) {
        element.innerHTML = element.innerHTML.replace(/#(\w+)/g, '<a href="/posts/?hashtag=$1" class="hashtag">#$1</a>');
    });
}); 