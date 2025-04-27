<template >
    <!-- <div class="navbar">
        <div @click="$router.push('/')">Vue 3</div>
        <div class="navbar__btns">
            <my-button @click="$router.push('/posts')">Посты</my-button>
            <my-button style="margin-left: 20px" @click="$router.push('/about')">О сайте</my-button>
            <my-button style="margin-left: 20px" @click="$router.push('/register')">Регистрация</my-button>
            <my-button style="margin-left: 20px" @click="$router.push('/login')">Вход</my-button>
        </div>
    </div> -->
    <nav class="navbar navbar-expand navbar-light fixed-top">
        <div class="container">
            <a href="#" class="navbar-brand">Home</a>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item">
                        <a href="/about" class="nav-link">About</a>
                    </li>
                    <li class="nav-item">
                        <a href="/posts" class="nav-link">Posts</a>
                    </li>
                    <li class="nav-item">
                        <a href="/login" class="nav-link">Login</a>
                    </li>
                    <li class="nav-item">
                        <a href="/register" class="nav-link">Sign up</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>
<script>
export default {
    
}
</script>
<style scoped>
.navbar {
    height: 50px;
    /* background-color: lightgray; */
    box-shadow: 2px 2px 4px gray;
    display: flex;
    align-items: center;
    padding: 0 15px;
}

.navbar__btns {
    margin-left: auto;
}
</style>