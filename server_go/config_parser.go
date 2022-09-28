package main

import (
	ini "gopkg.in/ini.v1"
)

type CfgCtx struct {
	protocol string
	port     string
	hostname string
}

func parse_cfg(filename string) (*CfgCtx, error) {
	f, err := ini.Load(filename)
	if err != nil {
		return nil, err
	}
	server_section, err := f.GetSection("server")
	if err != nil {
		return nil, err
	}

	protocol_key, err := server_section.GetKey("protocol")
	if err != nil {
		return nil, err
	}
	protocol := protocol_key.String()

	port_key, err := server_section.GetKey("port")
	if err != nil {
		return nil, err
	}
	port := port_key.String()

	hostname_key, err := server_section.GetKey("hostname")
	if err != nil {
		return nil, err
	}
	hostname := hostname_key.String()

	ctx := CfgCtx{
		protocol: protocol,
		port:     port,
		hostname: hostname,
	}

	return &ctx, nil
}
