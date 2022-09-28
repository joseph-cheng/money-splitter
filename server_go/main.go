package main

import "net"
import "fmt"

func create_listener(cfgCtx *CfgCtx) (net.Listener, error) {
  return net.Listen(cfgCtx.protocol, cfgCtx.port + ":" + cfgCtx.hostname);
}

func main() {
  cfgCtx, err := parse_cfg("../ms.ini")
  if (err != nil) {
    fmt.Println("unable to parse cfg");
    fmt.Println(err);
    return;
  }

  ln, err := create_listener(cfgCtx);
  if (err != nil) {
    fmt.Println("unable to create listener");
    fmt.Println(err);
    return;
  }

  run_server(ln);
}
