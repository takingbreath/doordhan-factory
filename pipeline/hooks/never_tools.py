#!/usr/bin/env python3
"""PreToolUse hook (.claude/settings.json) on tools this repo never uses, whatever the instructions in the session.
The matcher names them by suffix, because each person's connector carries its own ID (mcp__<id>__<tool>).
- Posting (hard rule 6: only Akhilesh posts): vidIQ's Instagram publish, YouTube upload and video edits, comment
  replies; Higgsfield's TikTok publishing and account links, project and website publishing.
- Voices on Higgsfield (hard rule 4 and CLAUDE.md "Voices"): cloning or changing a voice there. New voices are made on
  ElevenLabs, never from a real person's voice without their consent.
Exit 2 blocks the call and tells Claude why."""
import json, sys

POSTING = {"vidiq_instagram_publish_reel", "vidiq_video_upload", "vidiq_update_video", "vidiq_update_video_thumbnail",
           "vidiq_reply_to_comment", "vidiq_comment_reply_permission", "vidiq_authorize_with_youtube",
           "vidiq_connect_youtube_channel", "tiktok_prepare_publish", "tiktok_connect", "tiktok_reconnect",
           "publish_project", "unpublish_project", "update_project_publication", "confirm_project_publication_review",
           "save_project_publication_preview", "publish_website", "deploy_website", "participate_in_contest"}
VOICES = {"create_voice", "create_voice_from_confirmed_audio", "voice_change", "dubbing"}

try:
    tool = (json.load(sys.stdin).get("tool_name") or "")
except Exception:
    tool = ""
suffix = tool.split("__")[-1]
if suffix in VOICES:
    print(f"Blocked: {suffix} makes or changes a voice on Higgsfield. Voices are made on ElevenLabs (no credits), and "
          "never cloned from a real person without their consent (hard rule 4). Use the voice in registry/assets.json.",
          file=sys.stderr)
    sys.exit(2)
if suffix in POSTING or not suffix:  # unreadable input is blocked too
    print(f"Blocked: {suffix or 'this tool'} can post, publish or change a public account. Only Akhilesh posts "
          "(hard rule 6). Hand over the stamped final and the posting kit instead.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
