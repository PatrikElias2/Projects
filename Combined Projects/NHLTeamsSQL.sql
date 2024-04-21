select * from NHLTeams

ALTER TABLE NHLTeams
ALTER COLUMN Wins int;

ALTER TABLE NHLTeams
ALTER COLUMN Losses int;

ALTER TABLE NHLTeams
ALTER COLUMN OT_Losses int;

ALTER TABLE NHLTeams
ALTER COLUMN Goals_For int;

ALTER TABLE NHLTeams
ALTER COLUMN Goals_Against int;

ALTER TABLE NHLTeams
ALTER COLUMN Diff int;


--Returns the number of the wins and a year in which Boston Bruins scored maximum wins 
SELECT TOP 1 WITH TIES Year, MaxWins AS OverallMaxWins
FROM (
  SELECT Year, MAX(Wins) AS MaxWins
  FROM NHLTeams
  WHERE [Team Name] = 'Boston Bruins'
  GROUP BY Year
) AS Subquery
ORDER BY MaxWins DESC;


--Returns teams that had more wins than average wins in the specific year 
SELECT [Team Name], Year, Wins,
  (SELECT AVG(Wins)
   FROM NHLTeams AS Subquery
   WHERE Subquery.Year = NHLTeams.Year  -- Filter for same year
   GROUP BY Subquery.Year) AS AvgWinsThisYear
FROM NHLTeams
where Wins > (SELECT AVG(Wins)
   FROM NHLTeams AS Subquery
   WHERE Subquery.Year = NHLTeams.Year  -- Filter for same year
   GROUP BY Subquery.Year);


--Returns teams that had more losses than average losses in the specific year 
SELECT [Team Name], Year, Losses,
  (SELECT AVG(Losses)
   FROM NHLTeams AS Subquery
   WHERE Subquery.Year = NHLTeams.Year  -- Filter for same year
   GROUP BY Subquery.Year) AS AvgLossesThisYear
FROM NHLTeams
where Losses > (SELECT AVG(Losses)
   FROM NHLTeams AS Subquery
   WHERE Subquery.Year = NHLTeams.Year  -- Filter for same year
   GROUP BY Subquery.Year);


--Adding a column that calculates difference between wins and losses
ALTER TABLE NHLTeams
ADD WinLossDiff AS (Wins - Losses);

--Return only those teams that had positive Win/Loss difference
SELECT [Team Name], Year
FROM (
  SELECT [Team Name], Year, WinLossDiff
  FROM NHLTeams
) AS Subquery
WHERE WinLossDiff > 0  -- Filter for positive WinLossDiff only
GROUP BY [Team Name], Year
HAVING COUNT(*) = 1;  -- Ensure positive WinLossDiff in all years for a team


--Returns teams that scored more goals than average scored goals in each year
SELECT [Team Name], Year, Goals_for,
  (SELECT AVG(Goals_for)
   FROM NHLTeams AS Subquery
   WHERE Subquery.Year = NHLTeams.Year  -- Filter for same year
   GROUP BY Subquery.Year) AS AvgGoalsThisYear
FROM NHLTeams
where Goals_for > (SELECT AVG(Goals_for)
   FROM NHLTeams AS Subquery
   WHERE Subquery.Year = NHLTeams.Year  -- Filter for same year
   GROUP BY Subquery.Year);


--Return teams that had the lowest amount of goals received each year
SELECT [Team Name], Year, Goals_Against
FROM (
  SELECT [Team Name], Year, Goals_Against,
    ROW_NUMBER() OVER (PARTITION BY Year ORDER BY Goals_Against ASC) AS Rank
  FROM NHLTeams
) AS Subquery
WHERE Rank = 1;

