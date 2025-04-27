import axios from 'axios';

export const fetchUserProfile = async () => {
    try {
        const tokens = JSON.parse(localStorage.getItem('userTokens'));
        if (!tokens || !tokens.access_token) {
            throw new Error('Токен доступа отсутствует');
        }

        const response = await axios.get(`http://localhost:7777/auth/me`, {
            headers: {
                Authorization: `Bearer ${tokens.access_token}`
            }
        });

        return response.data; // Возвращаем данные о пользователе
    } catch (err) {
        console.error('Ошибка получения информации о пользователе:', err);
        throw err; // Пробрасываем ошибку дальше
    }
};
