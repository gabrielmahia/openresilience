from fastapi import APIRouter
router=APIRouter()
@router.get('')
def h():
    return {'ok': True}
