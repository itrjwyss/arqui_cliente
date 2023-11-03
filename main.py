import datetime

from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database import SessionLocal, engine
from model import Customer, Transaction


def get_database_session():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()


# @app.get("/")
# async def root(db: Session = Depends(get_database_session)):
#     return db.query(Autor).all()
#
#
# @app.get("/findById/{id}")
# async def say_hello(id: int, db: Session = Depends(get_database_session)):
#     return db.query(Autor).filter(Autor.id==id).first()
#
#
# @app.post("/create")
# async def create_autor(request: Request, db: Session = Depends(get_database_session)):
#     request_body = await request.json()
#
#     autor = Autor(
#         nombres=request_body['nombres'],
#         apellidos=request_body['apellidos'],
#         fecha_nac=request_body['fecha_nac']
#     )
#
#     db.add(autor)
#     db.commit()
#
#     return JSONResponse(
#         status_code=200,
#         content={
#             "successful": True,
#             "message": "Autor creado con éxito."
#         }
#     )


@app.post("/transaction")
async def create_transaction(request: Request, db: Session = Depends(get_database_session)):
    request_body = await request.json()

    customer = db.query(Customer).filter(Customer.id == request_body['client_id']).first()
    if customer is not None:
        if customer.frequent:
            if customer.points > 0:
                discount = customer.points

                customer.points = 0
                db.commit()
                db.refresh(customer)

                transaction = Transaction(
                    type="CANJEAR",
                    day=datetime.datetime.now(),
                    client_id=request_body['client_id']
                )

                db.add(transaction)
                db.commit()

                return JSONResponse(
                    status_code=200,
                    content={
                        "successful": True,
                        "message": "Transaccion realizada con éxito.",
                        "discount": discount
                    }
                )
            else :
                customer.points = request_body['galones'] / 5
                db.commit()
                db.refresh(customer)

                transaction = Transaction(
                    type="ACUMULAR",
                    day=datetime.datetime.now(),
                    client_id=request_body['client_id']
                )

                db.add(transaction)
                db.commit()

                return JSONResponse(
                    status_code=200,
                    content={
                        "successful": True,
                        "message": "Transaccion realizada con éxito.",
                        "discount": 0
                    }
                )
        else:
            transaction = Transaction(
                type="SIMPLE",
                day=datetime.datetime.now(),
                client_id=request_body['client_id']
            )

            db.add(transaction)
            db.commit()

            return JSONResponse(
                status_code=200,
                content={
                    "successful": True,
                    "message": "Transaccion realizada con éxito.",
                    "discount": 0
                }
            )
    else:
        return JSONResponse(
            status_code=200,
            content={
                "successful": False,
                "message": "El cliente de la transacción no existe."
            }
        )
