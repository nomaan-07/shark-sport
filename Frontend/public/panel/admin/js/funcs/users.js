const getAndShowAllUsers = async (isShow, pageNumber, limit) => {
  const skip = (pageNumber - 1) * limit;
  const response = await fetch(
    `http://localhost:8000/api/user/list_users/?show_deleted=${isShow}&skip=${skip}&limit=${limit}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const users = await response.json();
  console.log(response);
  console.log(users);
};

export { getAndShowAllUsers };
