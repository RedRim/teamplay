import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useRegisterStore = defineStore('auth', () => {
    const userInfo = ref({
        "username": '',
        "password": '',
        "last_name": '',
        "id": '',
        "first_name": '',
        "email": '',
        "user_type": '',
    })
    const error = ref('');
    const loader = ref(false);

    const signup = async (payload) => {
        error.value = '';
        loader.value = true;
        try {
            console.log(payload)
            let response = await axios.post(`http://localhost:7777/auth/register`, {
                ...payload
            });
            userInfo.value = {
                "username": response.data.username,
                "password": response.data.password,
                "last_name": response.data.last_name,
                "id": response.data.id,
                "first_name": response.data.first_name,
                "email": response.data.email,
                "user_type": response.data.user_type,
            }
            loader.value = false;
        } catch(err) {
            console.log('Ошибка');
            console.log(err.response.data.detail)
            switch (err.response.data.detail) {
                case 'Пользователь с таким именем уже существует':
                    error.value = 'Пользователь с таким именем уже существует';
                    break;
                default:
                    error.value = 'Произошла непредвиденная ошибка';
                    break;
            }
        } finally {
            loader.value = false;
        }
    }
    return { signup, userInfo, error, loader }
})