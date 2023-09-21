import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from mangum import Mangum


class Book(BaseModel):
    name: str
    genre: Literal["fiction", "non-fiction"]
    price: float
    book_id: Optional[str] = uuid4().hex,
    img: str


BOOKS_FILE = "books.json"
BOOKS = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOKS = json.load(f)

app = FastAPI()
handler = Mangum(app)


@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app!"}


@app.get("/random-book")
async def random_book():
    return random.choice(BOOKS)


@app.get("/list-books")
async def list_books():
    return {"books": BOOKS}


@app.get("/book_by_index/{index}")
async def book_by_index(index: int):
    if index < len(BOOKS):
        return BOOKS[index]
    else:
        raise HTTPException(404, f"Book index {index} out of range ({len(BOOKS)}).")


@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOKS.append(json_book)

    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOKS, f)

    return {"book_id": book.book_id}


@app.post("/add-bodok")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    print("json_book=====>", json_book)

    # BOOKS.append(json_book)

    # with open(BOOKS_FILE, "w") as f:
    #     json.dump(BOOKS, f)

    # return {"book_id": book.book_id}

# @ns.route("/Filter/Bilateral")
# class BilateralApi(Resource):  
#     @ns.expect(image_edit_input_model)
#     @ns.marshal_list_with(image_Edit_model)
#     def post(self):
#         img = readb64(ns.payload['img'])
#         gray_image = color.rgb2gray(img)
#         smoothed_image = denoise_bilateral(gray_image, sigma_color=0.05, sigma_spatial=15)
#         num_bins = 8
#         quantized_image = np.floor(smoothed_image * num_bins) / num_bins
#         bilateral_img = np.stack([quantized_image] * 3, axis=-1)
#         bilateral_img = img_as_ubyte(bilateral_img)
#         write_img = write64(bilateral_img)
#         response_img = {
#             'img': write_img,
#         }
#         return response_img, 200


@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOKS:
        if book.book_id == book_id:
            return book

    raise HTTPException(404, f"Book ID {book_id} not found in database.")

# app.run(debug=True, port=5005)