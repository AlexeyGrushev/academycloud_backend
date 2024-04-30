import asyncio
import argparse

from app.users.user_dao import UserDAO


async def update_user_role(user_id, role):
    """User role updater
    Only use as: python3 -m app.base.set_user_role {user_id} {new_role}
    Args:
        user_id (_type_): _description_
        role (_type_): _description_
    """
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        print("Такого пользователя не существует")
    print("USER:")
    print(
        f"Email: {user[0].email}",
        f"Login: {user[0].login}",
        f"Verification: {user[0].is_verified}",
        f"Role: {user[0].role}",
        sep="\n"
        )
    await UserDAO.update_user(
        user_id=int(user_id),
        role=int(role)
    )
    print(f"Now role setted to {role}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Обновление роли пользователя.')
    parser.add_argument('user_id', type=int, help='ID Пользователя')
    parser.add_argument('role', type=int, help='ID назначаемой роли')

    args = parser.parse_args()

    asyncio.run(update_user_role(
        args.user_id,
        args.role
        ))
