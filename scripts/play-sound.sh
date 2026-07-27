#!/usr/bin/env bash
# Play a plugin sound. Usage: play-sound.sh <notify|complete>
# User overrides (in ~/.claude/claude-bell/):
#   <name>.wav   - replace the sound itself
#   volume.txt   - playback volume 0-100 (default 100; 0 = mute)
# Never blocks or fails the hook: always exits 0.

name="$1"
[ -n "$name" ] || exit 0

# Resolve plugin root: env var from Claude Code, else relative to this script
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

file="$HOME/.claude/claude-bell/$name.wav"
[ -f "$file" ] || file="$root/sounds/$name.wav"
[ -f "$file" ] || exit 0

# Volume: integer 0-100 from volume.txt, default 100
vol=100
vol_file="$HOME/.claude/claude-bell/volume.txt"
if [ -f "$vol_file" ]; then
  v="$(tr -cd '0-9' < "$vol_file")"
  if [ -n "$v" ] && [ "$v" -le 100 ] 2>/dev/null; then
    vol="$v"
  fi
fi
[ "$vol" -eq 0 ] && exit 0

case "$(uname -s)" in
  Darwin)
    gain="$(LC_ALL=C awk -v v="$vol" 'BEGIN{printf "%.2f", v/100}')"
    afplay -v "$gain" "$file" >/dev/null 2>&1
    ;;
  Linux)
    paplay --volume=$((vol * 65536 / 100)) "$file" >/dev/null 2>&1 \
      || aplay -q "$file" >/dev/null 2>&1 \
      || ffplay -nodisp -autoexit -loglevel quiet -volume "$vol" "$file" >/dev/null 2>&1
    ;;
  MINGW*|MSYS*|CYGWIN*)
    winpath="$(cygpath -w "$file" 2>/dev/null || echo "$file")"
    # WPF MediaPlayer supports volume (SoundPlayer does not); wait until
    # playback ends, capped at 3s so a bad file can never stall the hook
    powershell.exe -NoProfile -Command "
      Add-Type -AssemblyName PresentationCore;
      \$p = New-Object System.Windows.Media.MediaPlayer;
      \$p.Open([Uri]'$winpath');
      \$p.Volume = $vol / 100;
      \$p.Play();
      \$deadline = (Get-Date).AddSeconds(3);
      Start-Sleep -Milliseconds 300;
      while ((Get-Date) -lt \$deadline) {
        if (\$p.NaturalDuration.HasTimeSpan -and \$p.Position -ge \$p.NaturalDuration.TimeSpan) { break }
        Start-Sleep -Milliseconds 100
      }
      \$p.Close()" >/dev/null 2>&1
    ;;
esac

exit 0
