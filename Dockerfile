FROM golang:1.10
LABEL MAINTAINER="Salih Çiftçi"

WORKDIR /go/src/tina
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

CMD ["tina"]