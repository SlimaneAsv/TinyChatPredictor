let userPatternDB = {};

// Function to update word patterns and save them to storage
function logWordSequence(previousWords, nextWord) {
  const key = previousWords.join(" ");
  if (!userPatternDB[key]) {
    userPatternDB[key] = {};
  }
  userPatternDB[key][nextWord] = (userPatternDB[key][nextWord] || 0) + 1;
  chrome.storage.local.set({ userPatternDB });
}

// Load the stored word patterns when the extension starts
chrome.storage.local.get("userPatternDB", (result) => {
  if (result.userPatternDB) {
    userPatternDB = result.userPatternDB;
  }
});

// Listen for messages from content.js to update word patterns
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "logWordSequence") {
    logWordSequence(message.previousWords, message.nextWord);
  }
});
