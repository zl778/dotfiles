#r/设计

蕉幻 AI原生PPT生成器
项目地址：https://github.com/Anionex/banana-slides

git clone [https://github.com/Anionex/banana-slides.git](https://github.com/Anionex/banana-slides.git)
cd banana-slides

cp .env.example .env
vim .env

docker compose -f docker-compose.prod.yml up -d

（遇到问题 Gemini 额度用完）


docker compose -f docker-compose.prod.yml down