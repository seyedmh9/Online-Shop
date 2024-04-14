import {
  Admin,
  Resource,
  ListGuesser,
  EditGuesser,
  ShowGuesser,
} from "react-admin";
import { dataProvider } from "./dataProvider";
import { authProvider } from "./authProvider";
import { UsersList } from "./resource db/Users";
import { UsersCreate } from "./resource db/Userscreate";

export const App = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
    <Resource
      name="Users"
      list={UsersList}
      edit={EditGuesser}
      show={EditGuesser}
      create={UsersCreate}
    />
  </Admin>
);
