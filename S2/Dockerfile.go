FROM golang:1.23 AS build 
WORKDIR /src

# creating "main.go" on fly under "/src" path
COPY <<EOF /src/main.go
package main
import "fmt"

func main(){
    fmt.Println("Hello, planet!!")
}
EOF

# compiling program "main.go" and save executable in "/bin/hello"
RUN go build -o /bin/hello ./main.go

# New OS
FROM scratch

# COPY build-Image "/bin/hello"  =>  scratch "/bin/hello"
COPY --from=build /bin/hello /bin/hello

# Execute
CMD [ "/bin/hello" ]

# docker build -f Dockerfile.go -t GolangImg:latest .
# docker run -it --rm GolangImg