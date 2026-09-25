# Setup

Give Claude Code the zip and the single prompt from the chat where this repo was built (repeated below).

---

You're taking over production of Doordhan, my all-AI finance reels channel on Instagram. Everything built so far is in doordhan-factory.zip: the channel's rules and lessons, two show templates (a news bulletin and a teleshop), working editing tools, and every asset ID. Unzip it into a folder named doordhan-factory in my home directory, and read CLAUDE.md first, then the formats, playbooks and pipeline README.

Set the system up so it runs day to day: put it in a private GitHub repo named doordhan-factory; get the pipeline running on this machine and passing its self-test; connect the Higgsfield MCP server at https://mcp.higgsfield.ai/mcp (I'll sign in when you ask) and bring the registry in line with what actually exists in my account, voices especially; confirm the ElevenLabs key in ELEVENLABS_API_KEY works without ever printing it, and update the voice tool if its model name is out of date; prove the whole chain with one short test shot of Sarika from the news template, spending no more than 10 credits, and check it yourself the way the repo describes; then set up the morning news desk as a cloud routine that emails me three story options at 7:30 am India time, Monday to Saturday, and ask me for the email address when you get there.

You have creative and technical freedom. The repo is what we've learned so far, not a cage: review it critically, and change any default, tool, playbook or template you think is wrong or will slow us down. Keep the hard rules in CLAUDE.md unless I agree to change them, and log what you change and why. Stop and ask me only for a sign-in, my email, or spending beyond the budgets in CLAUDE.md.

Done when: the repo is on GitHub, the self-test passes, the test shot's final video is in outputs/ with your quality notes, the routine has sent me one real email, and you've given me a short report of what you set up, what you changed in the repo and why, and the credits spent.
