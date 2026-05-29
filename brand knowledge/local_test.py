import litellm
import os

# Test with Gemini (assuming GEMINI_API_KEY is in env)
print("--- TESTING GEMINI ---")
gemini_models = ["gemini/gemini-2.5-flash", "gemini/gemini-2.0-flash", "gemini/gemini-1.5-flash-latest"]
for m in gemini_models:
    try:
        print(f"Testing {m}...")
        response = litellm.completion(model=m, messages=[{"role": "user", "content": "hi"}], max_tokens=2)
        print(f"  ✅ SUCCESS: {m}")
    except Exception as e:
        print(f"  ❌ FAILED: {m} - {e}")

print("\n--- TESTING CLAUDE ---")
# User's Claude Key isn't here, but I can check the identifier logic
claude_models = ["anthropic/claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20240620", "anthropic/claude-3-sonnet-20240229"]
for m in claude_models:
    print(f"Identifier logic check for: {m}")
    # We can't run a live test without the user's key here, but we can verify what LiteLLM expects.
