// Load patterns from storage when the script starts
chrome.storage.local.get("userPatternDB", (result) => {
  if (result.userPatternDB) {
    userPatternDB = result.userPatternDB;
  }
});

document.addEventListener('input', function (event) {
  const textArea = event.target;
  if (textArea.tagName === 'TEXTAREA' || textArea.tagName === 'INPUT') {
    const words = textArea.value.trim().split(" ");
    if (words.length > 1) {
      const previousWords = words.slice(-2); // Last two words as context
      const suggestion = suggestNextWord(previousWords.join(" "));
      displaySuggestion(suggestion, textArea);
    }
  }
});

function suggestNextWord(context) {
  const suggestions = userPatternDB[context];
  if (suggestions) {
    const sortedSuggestions = Object.entries(suggestions).sort((a, b) => b[1] - a[1]);
    return sortedSuggestions[0][0]; // Most common next word
  }
  return null;
}

function displaySuggestion(suggestedWord, textArea) {
  if (!suggestedWord) return;

  const suggestionBox = document.createElement('span');
  suggestionBox.id = 'suggestion-box';
  suggestionBox.style.position = 'absolute';
  suggestionBox.style.color = 'lightgrey';
  suggestionBox.textContent = ` ${suggestedWord}`;
  textArea.parentNode.insertBefore(suggestionBox, textArea.nextSibling);

  // Insert the word on pressing '²'
  document.addEventListener('keydown', function (event) {
    if (event.key === '²') {
      textArea.value += suggestedWord + ' ';
      suggestionBox.remove();
    }
  });
}
