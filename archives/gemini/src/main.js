import './style.css';

document.addEventListener('DOMContentLoaded', () => {
    const imageSlider = document.querySelector('.image-slider');
    if (imageSlider) {
        let scrollPosition = 0;
        const images = imageSlider.querySelectorAll('img');
        const imageWidth = images[0]?.offsetWidth || 600; // 默认宽度

        setInterval(() => {
            scrollPosition += imageWidth;
            if (scrollPosition >= imageWidth * images.length) {
                scrollPosition = 0;
            }
            imageSlider.scrollTo({ left: scrollPosition, behavior: 'smooth' });
        }, 3000); // 每 3 秒切换一次图片
    }

    // 添加关注按钮的交互
    const followButtons = document.querySelectorAll('.follow-button');
    followButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('following');
            button.textContent = button.classList.contains('following') ? '已关注' : '关注';
        });
    });
});