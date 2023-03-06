-- Creation database 
CREATE DATABASE `g5` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
show tables ;

-- g5.Users definition
CREATE TABLE `Users` (
  `username` varchar(50) NOT NULL,
  `user_id` int DEFAULT NULL,
  `country` varchar(5) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  `level_of_education` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- g5.Mooc definition
CREATE TABLE `Mooc` (
  `course_id` varchar(50) NOT NULL,
  `opening_date` date DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- g5.Results definition
CREATE TABLE `Results` (
  `course_id` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `grade` float NOT NULL,
  `certificate_eligible` varchar(1) NOT NULL,
  PRIMARY KEY (`course_id`,`username`),
  KEY `Results_FK_1` (`username`),
  CONSTRAINT `Results_FK` FOREIGN KEY (`course_id`) REFERENCES `Mooc` (`course_id`),
  CONSTRAINT `Results_FK_1` FOREIGN KEY (`username`) REFERENCES `Users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- g5.Threads definition
CREATE TABLE `Threads` (
  `_id` char(24) NOT NULL,
  `course_id` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  KEY `Threads_FK` (`course_id`),
  CONSTRAINT `Threads_FK` FOREIGN KEY (`course_id`) REFERENCES `Mooc` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- g5.Messages definition
CREATE TABLE `Messages` (
  `id` char(24) NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `depth` smallint DEFAULT NULL,
  `thread_id` char(24) DEFAULT NULL,
  `body` text,
  `parent_id` char(24) DEFAULT NULL,
  `body_length` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Messages_FK` (`username`),
  KEY `Messages_FK_1` (`thread_id`),
  KEY `Messages_FK_2` (`parent_id`),
  CONSTRAINT `Messages_FK` FOREIGN KEY (`username`) REFERENCES `Users` (`username`),
  CONSTRAINT `Messages_FK_1` FOREIGN KEY (`thread_id`) REFERENCES `Threads` (`_id`),
  CONSTRAINT `Messages_FK_2` FOREIGN KEY (`parent_id`) REFERENCES `Messages` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- NB: possible que la table message ne puisse pas etre crée d'un coup. il faut d'abord la créer vide avec ses colonnes, 
-- puis ajouter la clé primaure sur id, puis ajouter les clés étrangères. Je pense que tout du'n coup ne marche pas car tant que la ligne n'est pas finie, 
-- il considère qu'il n'y a pas encore de clé primaire sur id et donc il ne veut pas mettre une clé étrangère sur parent_id qui pointe vers id 
-- (vu que clé primaire n'existe pas encore sur id)

/*
CREATE TABLE `Messages` (
  `id` char(24) NOT NULL,
  `type` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `depth` smallint DEFAULT NULL,
  `thread_id` char(24) DEFAULT NULL,
  `body` text,
  `parent_id` char(24) DEFAULT NULL,
  `body_length` int DEFAULT NULL);
  
 
-- manque ligne pour créer primary key sur id

ALTER TABLE g5_sylvine.Messages ADD CONSTRAINT Messages_FK FOREIGN KEY (username) REFERENCES g5_sylvine.Users(username);
ALTER TABLE g5_sylvine.Messages ADD CONSTRAINT Messages_FK_1 FOREIGN KEY (thread_id) REFERENCES g5_sylvine.Threads(`_id`);
ALTER TABLE g5_sylvine.Messages ADD CONSTRAINT Messages_FK_2 FOREIGN KEY (parent_id) REFERENCES g5_sylvine.Messages (id) 
*/




