#!/usr/bin/env bash
# Usage: ./release.sh 0.1.1  -- bump, tag, push, puis met a jour le sha256 de la formule.
set -euo pipefail
VERSION="${1:?usage: ./release.sh X.Y.Z}"
cd "$(dirname "$0")"
REMOTE_URL="$(git remote get-url origin | sed -E 's#(git@github.com:|https://github.com/)##; s#\.git$##')"

sed -i.bak -E "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml
sed -i.bak -E "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" src/ytsub/__init__.py
sed -i.bak -E "s#(archive/refs/tags/)v[0-9.]+(\.tar\.gz)#\1v$VERSION\2#" Formula/ytsub.rb
rm -f pyproject.toml.bak src/ytsub/__init__.py.bak Formula/ytsub.rb.bak

git add -A && git commit -m "Release v$VERSION" && git tag "v$VERSION"
git push origin HEAD "v$VERSION"

SHA="$(curl -fsSL "https://github.com/$REMOTE_URL/archive/refs/tags/v$VERSION.tar.gz" | shasum -a 256 | cut -d' ' -f1)"
SHA="$SHA" perl -0pi -e 's/sha256 "[^"]*"/sha256 "$ENV{SHA}"/' Formula/ytsub.rb  # 1re occurrence = le tarball du projet
git add -A && git commit -m "ytsub $VERSION: sha256 du tarball" && git push origin HEAD
echo "OK -> brew update && brew upgrade ytsub"
