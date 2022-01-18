package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func main() {
	res, err := http.Get("https://www.ovh.com/engine/api/dedicated/server/availabilities?country=fr")
  
	if err != nil {
		log.Fatal(err)
	}
  
	body, err := ioutil.ReadAll(res.Body)
	res.Body.Close()
  
	if err != nil {
		log.Fatal(err)
	}
  
	fmt.Printf("%s", body)
}
