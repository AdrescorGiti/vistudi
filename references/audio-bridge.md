# Audio and manual bridge

`python -m vistudi speak --text-file narration.txt --output voice.wav` uses installed eSpeak NG or eSpeak locally, then checks the WAV with ffprobe and ffmpeg. Specify `--voice` only for a voice installed locally. This is synthetic speech, not an ElevenLabs voice. Output must not already exist.

`python -m vistudi import-audio SOURCE DESTINATION` verifies that an existing local file contains audio and decodes, then copies it without overwriting. This allows a human to bring in a ChatGPT or other service's downloaded result; it does not authenticate to, send messages to, or generate audio through ChatGPT. Verify origin, rights, content and actual quality separately. No ElevenLabs API or automatic ChatGPT bridge is implemented. If a separately available service is used outside this CLI, discover its real capabilities, authorization, cost and usage rights first; do not spend paid credits without permission. Never put secrets in handoffs or output files.

The sound producer supplies wording, pronunciation, pacing and cue sheet even when no audio can be generated. Record actual audio format and duration, and pass the verified path to the editor. Technical decoding does not verify intelligibility, clipping, sync or rights.
