import {
  CreateButton,
  Datagrid,
  FilterButton,
  FilterForm,
  ListBase,
  List,
  Pagination,
  TextField,
  TextInput,
  SearchInput,
  EmailField,
  DateField,
  ReferenceField,
  ShowButton,
  DeleteButton
} from "react-admin";
import { Stack } from "@mui/material";

const Order_detailsFilters = [
  <SearchInput source="name" alwaysOn />,
  <TextInput label="email" source="email" defaultValue="irmrbug@gmail.com" />,
];
const ListToolbar = () => (
  <Stack direction="row" justifyContent="space-between">
    <FilterForm filters={Order_detailsFilters} />
    <div>
      <FilterButton filters={Order_detailsFilters} />
      <CreateButton />
    </div>
  </Stack>
);
export const Payment_list = () => (
  <List>
    <ListToolbar />
    <Datagrid rowClick="edit">
      <TextField source="payment_id" />
      <ReferenceField source="order_id" reference="Orders" link="show" />
      <TextField source="payment_method" />
      <TextField source="amount" />
      <TextField source="payment_date" />
      <ShowButton label="Show"/>
      <DeleteButton label="Delete"/>
    </Datagrid>
  </List>
);
