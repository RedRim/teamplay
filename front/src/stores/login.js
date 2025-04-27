import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useLoginStore = defineStore('auth', () => {
    const userInfo = ref({
        "access_token": '',
        "refresh_token": '',
        "token_type": '',
    })
    const userProfile = ref(null);
    const error = ref('');
    const loader = ref(false);

    const login = async (payload) => {
        error.value = '';
        loader.value = true;
        try {
            console.log(payload)
            let response = await axios.post(`http://localhost:7777/auth/login`, null, {
                auth: {
                    ...payload
                }
            });
            userInfo.value = {
                "access_token": response.data.access_token,
                "refresh_token": response.data.refresh_token,
                "token_type": response.data.token_type,
            }
            localStorage.setItem('userTokens', JSON.stringify({
                access_token: userInfo.value.access_token,
                refresh_tocken: userInfo.value.refresh_token
            }))
            await fetchUserProfile();
        } catch(err) {
            console.log('Ошибка');
            console.log(err.response.data.detail)
            switch (err.response.data.detail) {
                case 'Пользователь не найден':
                    error.value = 'Пользователь не найден';
                    break;
                case 'Неверный пароль':
                    error.value = 'Неверный пароль';
                    break;
                default:
                    error.value = 'Произошла непредвиденная ошибка';
                    break;
            }
            throw error.value;
        } finally {
            loader.value = false;
        }
    }

    const fetchUserProfile = async () => {
        try {
            const tokens = JSON.parse(localStorage.getItem('userTokens'));

            const response = await axios.get(`http://localhost:7777/auth/me`, {
                headers: {
                    Authorization: `Bearer ${tokens.access_token}`
                }
            });
            userProfile.value = response.data;
        } catch (err) {
            console.error('Ошибка получения информации о пользователе:', err);
        }
    };

    return { login, userInfo, userProfile, error, loader }
})