import re


class UpaMatrixBuilder:
    @classmethod
    def load_from_one2one_file(cls, filename: str):
        num_of_users = 0
        num_of_permissions = 0
        with open(filename, "r") as file:
            for line in file:
                user_num, permission_num = re.sub(r"\s+", " ", line.strip()).split(" ")
                num_of_users = (
                    int(user_num) if int(user_num) > num_of_users else num_of_users
                )
                num_of_permissions = (
                    int(permission_num)
                    if int(permission_num) > num_of_permissions
                    else num_of_permissions
                )

            file.seek(0)

        print(f"Users: {num_of_users}, Permissions: {num_of_permissions}")


if __name__ == "__main__":
    import time

    start_time = time.time()

    UpaMatrixBuilder.load_from_one2one_file("real_datasets/americas_large.txt")

    print("--- %s seconds ---" % (time.time() - start_time))
