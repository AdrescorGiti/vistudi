import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from vistudi import studio

class StudioTests(unittest.TestCase):
    def test_fallback_writes_five_pending_handoffs(self):
        with tempfile.TemporaryDirectory() as d:
            workspace = Path(d) / 'run'
            result = studio.run('A brief', workspace)
            self.assertEqual(result['mode'], 'limited')
            self.assertEqual(len(result['roles']), 5)
            self.assertTrue(all(x['status'] == 'not_dispatched' for x in result['roles']))
            self.assertEqual(len(list((workspace / 'handoffs').glob('*.md'))), 5)

    def test_local_provider_dispatch_and_failure_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            fake = Path(d) / 'codex'
            fake.write_text('#!/bin/sh\nwhile [ "$1" != "-o" ]; do shift; done\nshift\nprintf "actual response" > "$1"\n')
            fake.chmod(0o755)
            result = studio.run('brief', Path(d) / 'run', provider='ollama', executable=str(fake))
            self.assertEqual(result['mode'], 'delegated')
            self.assertTrue(all(x['status'] == 'completed' for x in result['roles']))
            self.assertEqual(len({x['output'] for x in result['roles']}), 5)
            fake.write_text('#!/bin/sh\nexit 1\n')
            result = studio.run('brief', Path(d) / 'failed', provider='ollama', executable=str(fake))
            self.assertEqual(result['mode'], 'limited')
            self.assertTrue(all(x['status'] == 'failed' for x in result['roles']))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'ffmpeg required')
    def test_media_qa_checks_real_media(self):
        with tempfile.TemporaryDirectory() as d:
            media = Path(d) / 'test.wav'
            subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440:duration=0.2','-y',str(media)], check=True)
            report = studio.media_qa(media)
            self.assertEqual(report['status'], 'passed')
            self.assertGreater(report['duration'], 0)
            self.assertEqual(report['streams'][0]['codec_type'], 'audio')
            self.assertEqual(studio.media_qa(Path(d) / 'missing.wav')['status'], 'failed')

    @unittest.skipUnless(shutil.which('espeak-ng') or shutil.which('espeak'), 'espeak required')
    def test_local_speech_and_import_are_verified(self):
        with tempfile.TemporaryDirectory() as d:
            audio = Path(d) / 'speech.wav'
            studio.speak('Hello', audio)
            self.assertEqual(studio.media_qa(audio)['status'], 'passed')
            copied = Path(d) / 'import.wav'
            studio.import_audio(audio, copied)
            self.assertEqual(audio.read_bytes(), copied.read_bytes())
            with self.assertRaises(ValueError):
                studio.import_audio(Path(d) / 'bad', copied)

if __name__ == '__main__': unittest.main()

class FailureTests(unittest.TestCase):
    def test_missing_codex_is_visible(self):
        with tempfile.TemporaryDirectory() as d:
            result = studio.run('brief', Path(d) / 'run', provider='ollama', executable='/nonexistent/codex')
            self.assertEqual(result['mode'], 'limited')
            self.assertEqual(result['roles'][0]['reason'], 'FileNotFoundError')

    def test_existing_workspace_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileExistsError):
                studio.run('brief', Path(d))
