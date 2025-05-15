from fastapi import APIRouter, Response, status

router = APIRouter(tags=['health'])


@router.get('')
async def health_status():
    return Response(content='ready', status_code=status.HTTP_200_OK)
