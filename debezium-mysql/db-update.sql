CREATE TABLE "mercatotestalter" (
  "id" SERIAL PRIMARY KEY, 
  "name" varchar(160)
);

ALTER TABLE "users" DROP COLUMN "country_code";