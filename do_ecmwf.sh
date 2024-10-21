#!/usr/bin/env bash

### Paths, some unnecessary.
readonly scriptName=$(basename "${BASH_SOURCE[0]}")
readonly scriptDir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)
### path to python interpretor 
readonly pyPath=~/miniconda3/envs/iceinfo_env/bin
### path to iceinfo scripts
readonly pyScriptPath=/mnt/c/MEGAsync/progs/scripts/iceinfo/scripts
### path to the grib2 files
readonly gribPath=${pyScriptPath}/sample
readonly newFigPath=${pyScriptPath}/test_fig

set -Eeuo pipefail
trap cleanup SIGINT SIGTERM ERR EXIT
### other signals to catch, refer to here ###
### https://opensource.com/article/20/6/bash-trap ###

### some functions: msg, and bye
msg() {
  echo >&2 -e "${1-}"
}

bye() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  echo ""
  usage
  exit "$code"
}

usage() {
  cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [-v] [-f] date zhr
where:
the arguments date and zhr are used to find the grib/nc files. 
   date is the date in YYYYmmdd string
   zhr is either 00 or 12
-h, --help      Print this help and exit
-v, --verbose   Print script debug info usin -x
-f, --flag      flag whether to do grib2nc conversion, default is true, so use -f flag to skip grib2nc (useful when "old" grib files are moved to a different folder) 
Note: loops through the flags but not capable to combine flags like -hv. 
Note2: flags must come before the arguments. 
Suggestion: could use flags to decide whether to do weather maps only or do waves etc.
EOF
  exit
}

cleanup() {
  xcode=$?
  echo "the exit code is ${xcode}."
  ### trap all and decide on cleanup action using exit code
  trap - SIGINT SIGTERM ERR EXIT
  ### script cleanup here
  ### if errors, remove empty dirs
  cd ${pyScriptPath} 
  find . -mindepth 1 -type d -empty -delete
  # e.g., rm -rf $TMP or something like this.
}

parse_args() {
  ### default values of variables set from params
  flag=1

  while :; do
    ### uncomment to know what is happening in this loop
    ### especially when adding more parameters
    # echo "${@}"
    case "${1-}" in
    -h | --help) usage ;;
    -v | --verbose) set -x ;;
    -f | --flag) flag=0 ;; # whether to do grib2nc
    ### optional param example below, not used here. 
    ##  -p | --param) # example named parameter
    ##   param="${2-}"
    ##   shift
    ##   ;;
    -?*) bye "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  ### all args in sep strings
  args=("$@")

  ### check required params (empty or not) and arguments (the number of args)
  [[ ${#args[@]} -lt 2 ]] && bye "Missing script arguments date and zhr"
  date=${args[0]}
  zhr=${args[1]}
  return 0
}

### parse args 
parse_args "$@"
msg "- arguments: ${args[*]-}" # or ${args[@]}

cd ${gribPath}
# ### script logic here
if [[ $flag -eq 1 ]];
then
echo 'I do the grib'
  atm_f=${date}-${zhr}-sfc.grib2
  atm_nc=${atm_f%.grib2}.nc
  wave_f=${date}-${zhr}-wave.grib2
  wave_nc=${wave_f%.grib2}.nc
  printf "\ngrib_to_netcdf sfc\n"
  ${pyPath}/grib_to_netcdf -o "${atm_nc}" "${atm_f}" 
  printf "\nnow waves\n\n"
  ${pyPath}/grib_to_netcdf -o "${wave_nc}" "${wave_f}"
else
echo 'I dont do the grib'
fi

cd ${pyScriptPath}
printf "\ndo Python plot scripts.\n\n"
${pyPath}/python plotECMWF-LHB.py "${date}" "${zhr}"
${pyPath}/python plotECMWFWave-LHB.py "${date}" "${zhr}"
printf "\n"

printf "\nrsync to the shared folder..\n\n"
### move to Shirase shared directory.
#rsync -auv ${newFigPath}/figure/ ~/symlinks/ecmwf/figure/

