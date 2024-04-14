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
import { CategoryList } from "./resource db/category";
import { CategoryCreat } from "./resource db/categoryCreat";
export const App = () => (
  <Admin dataProvider={dataProvider} authProvider={authProvider}>
    <Resource
      name="Users"
      list={UsersList}
      edit={EditGuesser}
      show={EditGuesser}
      create={UsersCreate}
    />
    <Resource
      name="Categories"
      list={CategoryList}
      edit={EditGuesser}
      show={ShowGuesser}
      create={CategoryCreat}
    />
  </Admin>
);
