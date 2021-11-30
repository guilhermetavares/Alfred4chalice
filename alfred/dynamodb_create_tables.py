from alfred.auth.models import BasicAuthUser


def dynamodb_create_tables():
    if not BasicAuthUser.exists():
        BasicAuthUser.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


if __name__ == "__main__":
    dynamodb_create_tables()
