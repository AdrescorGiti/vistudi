# ViStudi

ViStudi is a video production skill with a coordinator and exactly five permanent specialist roles. The coordinator remains responsible for reviewing and integrating their work.

1. [Creative Director and Brief Owner](agents/01-director/README.md)
2. [Visual Designer and Asset Steward](agents/02-visual-designer/README.md)
3. [Storyboard, Motion, and Edit Specialist](agents/03-story-editor/README.md)
4. [Sound, Voice, and Music Producer](agents/04-sound-producer/README.md)
5. [Production Pipeline and Quality Engineer](agents/05-pipeline-qa/README.md)

## Run locally

Requires Python 3.10+, ffmpeg and ffprobe. Local speech additionally requires eSpeak NG or eSpeak. Run from the repository root:

```sh
python -m vistudi run --brief brief.md --workspace /tmp/vistudi-project
python -m vistudi qa /path/to/export.mp4
python -m vistudi speak --text-file narration.txt --output /tmp/voice.wav
python -m vistudi import-audio /path/to/received.wav /tmp/imported.wav
python -m unittest discover -s tests -v
```

The workspace must not exist already. The default run creates five handoffs and `status.json` in **limited** mode; it does not call a model or pretend specialists worked. The coordinator can use those handoffs for manual work.

To explicitly run five sequential, separate real Codex CLI sessions, install and configure Codex and a local Ollama or LM Studio provider, then add `--local-provider ollama` or `--local-provider lmstudio`. This uses `codex exec --oss --local-provider` in read-only mode; each session produces a separate response file. The local server and model must already be available. Sessions are independent, not native child subagents of this coordinator; downstream integration and evaluation remain manual. The coordinator records failures and reports limited mode if any session fails. Provider configuration and execution can have resource or other costs; verify them before opting in. The project makes no cloud model calls itself. Never opt in when doing so would incur unapproved costs.

QA reports ffprobe metadata, positive duration, and a full ffmpeg audio/video decode; its `passed` means only these checks passed. It does not judge content, sync, clipping, rights, or visual quality. Audio import verifies and copies an existing local file: it is a manual handoff, not a ChatGPT connection. The eSpeak adapter generates local WAV speech; it does not offer ElevenLabs or claim voice licensing. See [audio details](references/audio-bridge.md), [production contract](references/production.md), and [SKILL.md](SKILL.md).

## Verification limits

Tests generate real audio locally for QA and eSpeak when installed. The Codex command integration is tested with a local stand-in executable; CI does not launch models or prove that a particular user's local provider is configured. No paid service credentials are required.
