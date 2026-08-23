#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s PID\n' "$0" >&2
  printf 'Inspect a running process owned by the current user.\n' >&2
}

if [[ $# -ne 1 || ! "$1" =~ ^[1-9][0-9]*$ ]]; then
  usage
  exit 2
fi

pid=$1
proc_dir="/proc/$pid"

if [[ ! -d "$proc_dir" ]]; then
  printf 'Process %s is not running or /proc is unavailable.\n' "$pid" >&2
  exit 1
fi

process_uid=$(stat -c '%u' "$proc_dir")
current_uid=$(id -u)
if [[ "$process_uid" != "$current_uid" ]]; then
  printf 'Refusing to inspect PID %s: it is not owned by the current user.\n' "$pid" >&2
  exit 1
fi

printf '%s\n' '--- ps summary ---'
ps -o user,pid,ppid,stat,etime,time,%cpu,vsz,rss,comm,args -p "$pid"

printf '%s\n' '--- executable and command line ---'
printf 'exe: '
readlink "$proc_dir/exe" || printf '[unavailable]\n'
printf 'cmdline: '
tr '\0' ' ' <"$proc_dir/cmdline"
printf '\n'

printf '%s\n' '--- selected /proc status fields ---'
while IFS= read -r line; do
  case "$line" in
    Name:*|State:*|Pid:*|PPid:*|Threads:*|VmPeak:*|VmSize:*|VmRSS:*|RssAnon:*|RssFile:*|voluntary_ctxt_switches:*|nonvoluntary_ctxt_switches:*)
      printf '%s\n' "$line"
      ;;
  esac
done <"$proc_dir/status"

printf '%s\n' '--- scheduler wait channel ---'
printf 'wchan: '
if ! tr -d '\n' <"$proc_dir/wchan"; then
  printf '[unavailable]'
fi
printf '\n'

printf '%s\n' '--- file descriptors ---'
for fd_path in "$proc_dir"/fd/*; do
  [[ -e "$fd_path" || -L "$fd_path" ]] || continue
  printf '%s -> ' "${fd_path##*/}"
  readlink "$fd_path" || printf '[unavailable]\n'
done

printf '%s\n' '--- first 12 memory mappings ---'
sed -n '1,12p' "$proc_dir/maps"
