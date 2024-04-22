import * as React from 'react';
import { Create, SimpleForm, TextInput, DateInput, required ,NumberInput,
    ImageInput , ImageField} from 'react-admin';

export const ProductCreate = (props:any) => (
<Create{...props}>
    <SimpleForm>
        <TextInput source="name" validate={[required()]} />
        <TextInput multiline source="description" validate={[required()]} />
        <TextInput source="price" validate={[required()]} />
        <TextInput source="category_id" validate={[required()]}  />
        <ImageInput source="picture" accept="image/*">
            <ImageField source="src" title="title" />
        </ImageInput>
    </SimpleForm>
</Create>
)



