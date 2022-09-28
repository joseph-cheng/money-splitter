package main

import (
	"encoding/binary"
	"net"
)

const (
	DERIVE_LENGTH = 0
  PASSWORD_HASH string = "hJp\xad\x94}\xe8r\xf5\x950\xbf\xc7\xbe:f7\x03\x85\xe0\xe8=\xc9\x03:\x0e\xc7\x06j\xe2'\x13"
  AUTH_FAILURE = '\x00'
  AUTH_SUCCESS = '\x01'
)

func run_server(ln net.Listener) {
	for {
		conn, err := ln.Accept()
		if err != nil {
		} else {
			go handle_client(conn)
		}
	}
}

func check_hash_match(bytes_to_check []byte, hash string) bool{
  // TODO
  return true;
}

func do_setup(conn net.Conn) error {
	for {
		password_bytes, err := recv_message(conn, DERIVE_LENGTH)
		if err != nil {
			return err
		}
    if check_hash_match(password_bytes, PASSWORD_HASH){  
      send_message(conn, []byte{AUTH_SUCCESS})
      break;
    }
    send_message(conn, []byte{AUTH_FAILURE})
	}
  return send_db(conn);
}

func send_db(conn net.Conn) error {
  return nil;
}

func send_message(conn net.Conn, data []byte) error {
  var bytes_sent_tot uint64 = 0
  for bytes_sent_tot < uint64(len(data)) {
    bytes_sent, err := conn.Write(data[bytes_sent_tot:])
    if (err != nil) {
      return err
    }
    bytes_sent_tot += uint64(bytes_sent);
  }
  return nil
}

func recv_message(conn net.Conn, length uint64) ([]byte, error) {
	if length == DERIVE_LENGTH {
		length_bytes, err := recv_message(conn, 4)
		if err != nil {
			return nil, err
		}
		// TODO: get this from config
		length = binary.BigEndian.Uint64(length_bytes)
	}

	data := make([]byte, length)
	var bytes_received_tot uint64 = 0
	for bytes_received_tot < length {
		bytes_received, err := conn.Read(data[bytes_received_tot:])
		if err != nil {
			return nil, err
		}
		bytes_received_tot += uint64(bytes_received)
	}

	return data, nil
}

func handle_client(conn net.Conn) {
  do_setup(conn);
}
