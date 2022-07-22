#!/bin/sh
git ls-files | grep '.py\|.sh\|.ui' | xargs cat | wc -l
