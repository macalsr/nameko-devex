#!/bin/bash

# DIR="${BASH_SOURCE%/*}"
# if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
# . "$DIR/nex-include.sh"

# to ensure if 1 command fails.. build fail
set -e

# ensure prefix is pass in
if [ $# -lt 1 ] ; then
	echo "NEX smoketest needs prefix"
	echo "nex-smoketest.sh acceptance"
	exit
fi

PREFIX=$1

# check if doing local smoke test
if [ "${PREFIX}" != "local" ]; then
    echo "Remote Smoke Test in CF"
    STD_APP_URL=${PREFIX}
else
    echo "Local Smoke Test"
    STD_APP_URL=http://localhost:8000
fi

echo STD_APP_URL=${STD_APP_URL}

# Test: Create Products
echo "=== Creating a product id: the_odyssey ==="
curl -s -XPOST  "${STD_APP_URL}/products" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": "the_odyssey", "title": "The Odyssey", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}'
echo

# Test: Get Product
echo "=== Getting product id: the_odyssey ==="
curl -s "${STD_APP_URL}/products/the_odyssey" | jq .
echo

echo "=== Creating a product id: the_enigma ==="
curl -s -XPOST  "${STD_APP_URL}/products" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": "the_enigma", "title": "the_enigma", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}'
echo

# Test: Get Products
echo "=== Getting list of products  ==="
curl -s "${STD_APP_URL}/products" | jq .
echo

# Test: Delete Product
echo "=== Deleting product id: the_odyssey ==="
    curl -s -X DELETE "${STD_APP_URL}/products/the_odyssey" | jq .
echo "=== Check if product id: the_odyssey was deleted==="
    curl -s "${STD_APP_URL}/products/the_odyssey" | jq .

echo

# Test: Update Product
echo "=== Update product id: the_odyssey ==="
echo "=== Creating a product id to test update: the_odyssey ==="
curl -s -XPOST  "${STD_APP_URL}/products" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"id": "the_odyssey", "title": "The Odyssey", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}'
echo
    curl -s -X PATCH "${STD_APP_URL}/products/the_odyssey" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"title": "The Odysseeey", "passenger_capacity": 101, "maximum_speed": 5, "in_stock": 10}'
echo
echo "=== Check if product id: the_odyssey was update==="
    curl -s "${STD_APP_URL}/products/the_odyssey" | jq .

echo
# Test: Create Order
echo "=== Creating Order ==="
ORDER_ID=$(
 curl -X POST "${STD_APP_URL}/orders" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "order_details": [
    {
      "product_id": "the_odyssey",
      "price": "100.99",
      "quantity": 1
    },
    {
      "product_id": "the_odyssey",
      "price": "100000.99",
      "quantity": 1
    }
    ]
  }'
  )
  echo "${STD_APP_URL}/orders" \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{"order_details": {"product_id": "gm-0.42695048845813344", "price": "100000.99", "quantity": 1}'

echo ${ORDER_ID}
ID=$(echo ${ORDER_ID} | jq '.id')

# Test: Get Order
echo "=== Getting Order ==="
echo ${ORDER_ID}
curl -s "${STD_APP_URL}/orders/${ID}" | jq .

# Test: Get Order
echo "=== Getting Orders ==="
curl -s "${STD_APP_URL}/orders" | jq .
echo

# Test: Delete Order
echo "=== Deleting order id: the_odyssey ==="
    curl -s -X DELETE "${STD_APP_URL}/orders/1" | jq .
echo "=== Check if order id: 1 was deleted==="
    curl -s "${STD_APP_URL}/orders/1" | jq .

echo
echo "=== Get orders by date ==="
curl -X GET  "${STD_APP_URL}/orders" \
  -H "Content-Type: application/json" \
  -d '{"initial_date": "2023-10-26T20:18:24.189615+00:00", "final_date": "2023-10-27T20:18:24.189615+00:00",
   "page": 1, "per_page": 10}'| jq .
echo
