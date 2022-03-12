FROM ubuntu:20.04 as build
ENV TZ=Asia/Tokyo

COPY . /usr/src/open_eeslism
WORKDIR /usr/src/open_eeslism

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y build-essential cmake
RUN cmake -B build
RUN cd build && make

FROM ubuntu:20.04
WORKDIR /root/
COPY --from=build /usr/src/open_eeslism/build/eeslism ./
CMD ["./eeslism"]
