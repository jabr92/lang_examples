import Data.List.Split

type Cell = Maybe Char
-- units are a row, column, or box
type Unit = (Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell)
type Grid = (Unit, Unit, Unit, Unit, Unit, Unit, Unit, Unit, Unit)

listToNonuple (a:b:c:d:e:f:g:h:[i]) = (a, b, c, d, e, f, g, h, i)

all_cell_nums = [1..81]

gridFromString :: String -> Grid
-- the grid is stored as a nonuple of rows
gridFromString s = listToNonuple $ map listToNonuple $ chunksOf 9 $ map toCell s
    where toCell '.' = Nothing
          toCell a   = Just a

getUnits :: Cell -> Grid -> (Unit, Unit, Unit)
getUnits _ = undefined

main = do
    let test = ".................85.7.1..2...........3...6.....9..523..6...3.1...18...54.4.69...7"
    putStrLn . show $ gridFromString test