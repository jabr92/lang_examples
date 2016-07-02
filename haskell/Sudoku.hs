import Data.List.Split

data Digit = 1|2|3|4|5|6|7|8|9
type Cell = Maybe Digit
type Unit = (Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell, Cell)
type Grid = (Unit, Unit, Unit, Unit, Unit, Unit, Unit, Unit, Unit)

fromString:: String -> Grid
fromString s = map toUnits $ chunksOf 9 $ chunksOf 3 $ map toCell s
	where toCell '.' = Nothing
		  toCell  a  = Just (read a :: Int)
		  toUnits (a:b:c:d:e:f:g:h:i) = ((a:d:g) (b:e:h) (c:f:i))
		  

getUnits:: Cell -> (Unit, Unit, Unit)



main = do
	let test = ".................85.7.1..2...........3...6.....9..523..6...3.1...18...54.4.69...7"