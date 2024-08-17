#!/bin/bash

if [ "$(type -t _lt)" != "function" ]; then
	source ~/money/.lt_complete;
fi

echo $*
