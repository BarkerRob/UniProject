CREATE TABLE stadium (
    stadium_id_pk INT AUTO_INCREMENT PRIMARY KEY,
    stadium_name VARCHAR(255) NOT NULL,
    x_coord DECIMAL(13,8) NOT NULL,
    y_coord DECIMAL(13,8) NOT NULL
);

CREATE TABLE team (
	team_id_pk INT AUTO_INCREMENT PRIMARY KEY,
    name_pk VARCHAR(255) NOT NULL,
    stadium_id_fk INT,
    CONSTRAINT fk_stadium
    FOREIGN KEY (stadium_id_fk)
		REFERENCES stadium(stadium_id_pk)
);

CREATE TABLE season_overview (
	team_id_pk_fk INT,
    season_pk INT,
    position INT,
    goals_for INT,
    goals_against INT,
    wins INT,
    draws INT,
    losses INT,
    PRIMARY KEY (team_id_pk_fk, season_pk),
    CONSTRAINT fk_team_id
    FOREIGN KEY (team_id_pk_fk)
		REFERENCES team(team_id_pk)
);

CREATE TABLE game (
	home_team_id_pk_fk INT,
    away_team_id_pk_fk INT,
    season_pk INT,
    matchday INT,
    home_team_score INT,
    away_team_score INT,
    PRIMARY KEY (home_team_id_pk_fk, away_team_id_pk_fk, season_pk),
    CONSTRAINT fk_home_team_id
    FOREIGN KEY (home_team_id_pk_fk)
		REFERENCES team(team_id_pk),
	CONSTRAINT fk_away_team_id
    FOREIGN KEY (away_team_id_pk_fk)
		REFERENCES team(team_id_pk)
);