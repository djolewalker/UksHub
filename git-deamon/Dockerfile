
FROM alpine:3.10.2

RUN apk add git-daemon 

CMD ["git", "daemon", "--reuseaddr", "--base-path=/var/lib/git", "/var/lib/git"]