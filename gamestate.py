## Goutham Karthi, Student ID: 19652712
class Cell:
    def __init__(self, contents: str):
        self._contents = contents

    def contents(self) -> str:
        '''returns contents of the cell'''
        return self._contents

    def state(self) -> str:
        '''determines the state of the cell(whether it is empty, faller, frozen, or landed, or matched)'''
        if self.contents() == ' ':
            return 'empty'
        elif self.contents()[0] == '[':
            return 'faller'
        elif self.contents()[0] == '|':
            return 'landed'
        elif self.contents()[0] == '*':
            return 'matched'
        elif len(self.contents()) == 1:
            return 'frozen'
        else:
            pass
        
    def matched(self) -> None:
        '''turns the cell into a matched cell'''
        if self.state() == 'frozen':
            self.update(('*' + self.contents() + '*'))
        elif self.state() == 'landed' or self.state() == 'faller':
            self.update(('*' + self.contents()[1] + '*'))

    def landed(self) -> None:
        '''turns the cell into a landed cell'''
        self.update('|' + self.contents()[1] + '|')

    def change_to_faller(self) -> None:
        '''turns the cell into a faller cell'''
        self.update('[' + self.contents()[1] + ']')

    def freeze(self) -> None:
        '''turns the cell into a frozen cell'''
        self.update(self.contents()[1])

    def update(self, value: str):
        '''given a value, updates the contents of the cell to the value'''
        self._contents = value

    def gem(self) -> str:
        '''returns the gem calue of the cell, without cell borders'''
        if self.state() == 'frozen':
            return self.contents()
        elif self.state() == 'landed' or self.state() == 'faller' or self.state() == 'matched':
            return self.contents()[1]

        

class Faller:
    def __init__(self, faller: str):
        self._column: int = int(faller[0]) - 1
        self._gems: list = faller[2:].split()
        for i in range(len(self._gems)):
            self._gems[i] = '[' + self._gems[i] + ']'

    def column_to_drop(self) -> int:
        '''returns the column number that the faller will be dropped in'''
        return self._column

    def gems(self) -> list:
        '''returns a list containing the gems in fall in order from top to bottom'''
        return self._gems

    def rotate(self) -> None:
        '''rotates the gems in the faller (third element become 1st, 1st becomes 2nd, and 2nd becomes 3rd)'''
        temp0 = self._gems[0]
        temp1 = self._gems[1]
        temp2 = self._gems[2]
        self._gems[0] = temp2
        self._gems[1] = temp0
        self._gems[2] = temp1

    def shift_right(self) -> None:
        '''shifts faller one step to the right'''
        self._column += 1

    def shift_left(self) -> None:
        '''shifts faller one step to the right'''
        self._column -= 1
        
class GameState:
    def __init__(self, contents: str):
        field_contents = contents.split('\n')
        field: list = []
        rows: int = len(field_contents)
        columns: int = len(field_contents[0])
        for i in range(rows):
            for j in range(columns):
                row: list = list(field_contents[i])
            field.append(row)
        self._field: list = field
        for i in range(rows):
            for j in range(columns):
                self._field[i][j] = Cell(self._field[i][j]) 

    def rows(self) -> int:
        '''returns number of rows in the field'''
        return len(self._field)

    def columns(self) -> int:
        '''returns number of columns in the field'''
        return len(self._field[0])
    
    def field(self) -> list:
        return self._field

    def display_field(self) -> None:
        '''prints string format of the field, with contents'''
        field_string: str = ''
        rows: int = len(self._field)
        columns: int = len(self._field[0])
        for i in range(rows):
            field_string += '|'
            for j in range(columns):
                if self._field[i][j].state() == 'landed' or self._field[i][j].state() == 'faller' or self._field[i][j].state() == 'matched':
                    field_string += self._field[i][j].contents()
                else:
                    field_string += ' ' + self._field[i][j].contents() + ' '
            field_string += '|\n'
        field_string += ' '
        for i in range(columns):
            field_string += '---'
        field_string += ' '
        print(field_string)

    def simplify_field(self) -> None:
        '''simplifies the field, so that holes are filled up, etc'''
        rows: int = len(self._field)
        columns: int = len(self._field[0])
        for i in range(rows-1):
            for j in range(columns):
                if self._field[i+1][j].state() == 'empty' and self._field[i][j].state() != 'empty':
                    temp = self._field[i][j].contents()
                    self._field[i+1][j].update(temp)
                    self._field[i][j].update(' ')
        for i in range(rows-1):
            for j in range(columns):
                if self._field[i+1][j].state() == 'empty' and self._field[i][j].state() != 'empty':
                    self.simplify_field()

    def matches(self) -> None:
        '''find matches of three in a row diagonally, vertically, or horizontally, and changes those cells to matched cells'''
        matches: bool = False
        for i in range(self.rows() - 1, -1, -1):
            for j in range(self.columns() - 2):
                if self.field()[i][j].state() != 'empty' and self.field()[i][j + 1].state() != 'empty' and self.field()[i][j + 2].state() != 'empty' and self.field()[i][j].gem() == self.field()[i][j + 1].gem() and self.field()[i][j].gem() == self.field()[i][j + 2].gem():
                    matches = True
                    self.field()[i][j].matched()
                    self.field()[i][j + 1].matched()
                    self.field()[i][j + 2].matched()
                    
            if matches == True:
                break
    
        if matches == True:
            self.display_field()
            return matches
        else:
            for i in range(self.rows() - 1, 1, -1):
                for j in range(self.columns()):
                    if self.field()[i][j].state() != 'empty' and self.field()[i - 1][j].state() != 'empty' and self.field()[i - 2][j].state() != 'empty' and self.field()[i][j].gem() == self.field()[i - 1][j].gem() and self.field()[i][j].gem() == self.field()[i - 2][j].gem():
                        matches = True
                        self.field()[i - 2][j].matched()
                        self.field()[i - 1][j].matched()
                        self.field()[i][j].matched()
                        break
        if matches == True:
            self.display_field()
            return matches
        else:
            for i in range(self.rows() - 2):
                for j in range(self.columns() - 2):
                    if self.field()[i][j].state() != 'empty' and self.field()[i + 1][j + 1].state() != 'empty' and self.field()[i + 2][j + 2].state() != 'empty' and self.field()[i][j].gem() == self.field()[i + 1][j + 1].gem() and self.field()[i][j].gem() == self.field()[i + 2][j + 2].gem():
                        matches = True
                        self.field()[i][j].matched()
                        self.field()[i + 1][j + 1].matched()
                        self.field()[i + 2][j + 2].matched()
                        break
        if matches == True:
            self.display_field()
            return matches
        else:
            for i in range(self.rows() - 2):
                for j in range(2, self.columns()):
                    if self.field()[i][j].state() != 'empty' and self.field()[i + 1][j - 1].state() != 'empty' and self.field()[i + 2][j - 2].state() != 'empty' and self.field()[i][j].gem() == self.field()[i + 1][j - 1].gem() and self.field()[i][j].gem() == self.field()[i + 2][j - 2].gem():
                        matches = True
                        self.field()[i][j].matched()
                        self.field()[i + 1][j - 1].matched()
                        self.field()[i + 2][j - 2].matched()
                        break
            self.display_field()
            return matches


            
    def remove_matches(self) -> None:
        '''clears all cells that have been matched'''
        for i in range(self.rows()):
            for j in range(self.columns()):
                if self.field()[i][j].state() == 'matched':
                    self.field()[i][j].update(' ')
        self.simplify_field()

                
                

    def drop_faller(self, faller: Faller, command_input: str) -> None or str:
        '''once faller has been created, this method takes care of all the commands until the faller has become frozen'''
        rows: int = len(self._field)
        columns: int = len(self._field[0])
        current_faller_row: int = 0
        for i in range(rows):
                if self._field[i][faller.column_to_drop()].state() == 'faller':
                    current_faller_row = i
                elif self._field[i][faller.column_to_drop()].state() == 'landed':
                    current_faller_row = i
        if command_input == '':
            temp: str = ''
            
            if current_faller_row == 0:
                if self._field[current_faller_row][faller.column_to_drop()].state() == 'landed':
                    self._field[current_faller_row][faller.column_to_drop()].freeze()
                    return 'faller has frozen'
                if not self._field[current_faller_row + 1][faller.column_to_drop()].state() == 'frozen':
                    temp = self._field[current_faller_row][faller.column_to_drop()].contents()
                    self._field[current_faller_row + 1][faller.column_to_drop()].update(temp)
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[1])
                    if self._field[current_faller_row + 2][faller.column_to_drop()].state() == 'frozen':
                        self._field[current_faller_row][faller.column_to_drop()].landed()
                        self._field[current_faller_row + 1][faller.column_to_drop()].landed()  
                else:
                    self._field[current_faller_row][faller.column_to_drop()].landed()

            elif current_faller_row == 1:
                if self._field[current_faller_row][faller.column_to_drop()].state() == 'landed':
                    self._field[current_faller_row - 1][faller.column_to_drop()].freeze()
                    self._field[current_faller_row][faller.column_to_drop()].freeze()
                    return 'faller has frozen'

                if not self._field[current_faller_row + 1][faller.column_to_drop()].state() == 'frozen':
                    temp = self._field[current_faller_row][faller.column_to_drop()].contents()
                    temp1 = self._field[current_faller_row - 1][faller.column_to_drop()].contents()
                    self._field[current_faller_row + 1][faller.column_to_drop()].update(temp)
                    self._field[current_faller_row][faller.column_to_drop()].update(temp1)
                    self._field[current_faller_row - 1][faller.column_to_drop()].update(faller.gems()[0])
                    if self._field[current_faller_row + 2][faller.column_to_drop()].state() == 'frozen':
                        self._field[current_faller_row - 1][faller.column_to_drop()].landed()
                        self._field[current_faller_row][faller.column_to_drop()].landed()
                        self._field[current_faller_row + 1][faller.column_to_drop()].landed()  
                else:
                    self._field[current_faller_row - 1][faller.column_to_drop()].landed()
                    self._field[current_faller_row][faller.column_to_drop()].landed()

            elif current_faller_row == rows - 1:
                self._field[current_faller_row][faller.column_to_drop()].freeze()
                self._field[current_faller_row - 1][faller.column_to_drop()].freeze()
                self._field[current_faller_row - 2][faller.column_to_drop()].freeze()
                return 'faller has frozen'
                

            elif current_faller_row >= 2:
                if self._field[current_faller_row][faller.column_to_drop()].state() == 'landed':
                    self._field[current_faller_row][faller.column_to_drop()].freeze()
                    self._field[current_faller_row - 1][faller.column_to_drop()].freeze()
                    self._field[current_faller_row - 2][faller.column_to_drop()].freeze()
                    return 'faller has frozen'

                if not self._field[current_faller_row + 1][faller.column_to_drop()].state() == 'frozen':
                    temp2 = self._field[current_faller_row][faller.column_to_drop()].contents()
                    temp1 = self._field[current_faller_row - 1][faller.column_to_drop()].contents()
                    temp0 = self._field[current_faller_row - 2][faller.column_to_drop()].contents()
                    self._field[current_faller_row + 1][faller.column_to_drop()].update(temp2)
                    self._field[current_faller_row][faller.column_to_drop()].update(temp1)
                    self._field[current_faller_row - 1][faller.column_to_drop()].update(temp0)
                    self._field[current_faller_row - 2][faller.column_to_drop()].update(' ')
                    if current_faller_row + 1 == rows - 1:
                        self._field[current_faller_row + 1][faller.column_to_drop()].landed()
                        self._field[current_faller_row][faller.column_to_drop()].landed()
                        self._field[current_faller_row - 1][faller.column_to_drop()].landed()
                    elif self._field[current_faller_row + 2][faller.column_to_drop()].state() == 'frozen':
                        self._field[current_faller_row + 1][faller.column_to_drop()].landed()
                        self._field[current_faller_row][faller.column_to_drop()].landed()
                        self._field[current_faller_row - 1][faller.column_to_drop()].landed()
                else:
                    self._field[current_faller_row][faller.column_to_drop()].landed()
                    self._field[current_faller_row-1][faller.column_to_drop()].landed()
                    self._field[current_faller_row-2][faller.column_to_drop()].landed()
            else:
                pass
           
        
        elif command_input[0] == 'F':
            self._field[0][faller.column_to_drop()].update(faller.gems()[2])
            if self._field[1][faller.column_to_drop()].state() == 'frozen':
                self._field[0][faller.column_to_drop()].landed()

        elif command_input == 'R':
            if current_faller_row == 0:
                if self._field[current_faller_row][faller.column_to_drop()].state() == 'faller':
                    faller.rotate()
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[2])
                elif self._field[current_faller_row][faller.column_to_drop()].state() == 'landed':
                    faller.rotate()
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[2])
                    self._field[current_faller_row][faller.column_to_drop()].landed()

                    
            elif current_faller_row == 1:
                if self._field[current_faller_row][faller.column_to_drop()].state() == 'faller':
                    faller.rotate()
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[2])
                    self._field[current_faller_row - 1][faller.column_to_drop()].update(faller.gems()[1])
                elif self._field[current_faller_row][faller.column_to_drop()].state() == 'landed':
                    faller.rotate()
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[2])
                    self._field[current_faller_row][faller.column_to_drop()].landed()
                    self._field[current_faller_row - 1][faller.column_to_drop()].update(faller.gems()[1])
                    self._field[current_faller_row - 1][faller.column_to_drop()].landed()

                    
            elif current_faller_row >= 2:
                if self._field[current_faller_row][faller.column_to_drop()].state() == 'faller':
                    faller.rotate()
                    self._field[current_faller_row - 2][faller.column_to_drop()].update(faller.gems()[0])
                    self._field[current_faller_row - 1][faller.column_to_drop()].update(faller.gems()[1])
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[2])
                elif self._field[current_faller_row][faller.column_to_drop()].state() == 'landed':
                    faller.rotate()
                    self._field[current_faller_row - 2][faller.column_to_drop()].update(faller.gems()[0])
                    self._field[current_faller_row - 2][faller.column_to_drop()].landed()
                    self._field[current_faller_row - 1][faller.column_to_drop()].update(faller.gems()[1])
                    self._field[current_faller_row - 1][faller.column_to_drop()].landed()
                    self._field[current_faller_row][faller.column_to_drop()].update(faller.gems()[2])
                    self._field[current_faller_row][faller.column_to_drop()].landed()

                    
        elif command_input == '>':
            if faller.column_to_drop() != self.columns() - 1:
                is_blocked_to_the_right: bool = False
                for i in range(self.rows()):
                    if self._field[i][faller.column_to_drop()].state() == 'faller' or self._field[i][faller.column_to_drop()].state() == 'landed':
                        if self._field[i][faller.column_to_drop() + 1].state() != 'empty':
                            is_blocked_to_the_right = True
                if is_blocked_to_the_right == False:
                    faller.shift_right()
                    for i in range(self.rows()):
                        if self._field[i][faller.column_to_drop() - 1].state() == 'faller' or self._field[i][faller.column_to_drop() - 1].state() == 'landed':
                            temp = self._field[i][faller.column_to_drop() - 1].contents()
                            self._field[i][faller.column_to_drop()].update(temp)
                            self._field[i][faller.column_to_drop() - 1].update(' ')
                    for j in range(self.rows() - 1):
                        if self._field[j][faller.column_to_drop()].state() == 'landed' and self._field[j + 1][faller.column_to_drop()].state() == 'empty':
                            for k in range(j + 1):
                                if self._field[k][faller.column_to_drop()].state() == 'landed':
                                    self._field[k][faller.column_to_drop()].change_to_faller()
                        if self._field[j][faller.column_to_drop()].state() == 'faller' and self._field[j + 1][faller.column_to_drop()].state() == 'frozen':
                            for k in range(j + 1):
                                if self._field[k][faller.column_to_drop()].state() == 'faller':
                                    self._field[k][faller.column_to_drop()].landed()
            else:
                pass
                                              
        elif command_input == '<':
            if faller.column_to_drop() != 0:
                is_blocked_to_the_left: bool = False
                for i in range(self.rows()):
                    if self._field[i][faller.column_to_drop()].state() == 'faller' or self._field[i][faller.column_to_drop()].state() == 'landed':
                        if self._field[i][faller.column_to_drop() - 1].state() != 'empty':
                            is_blocked_to_the_left = True
                if is_blocked_to_the_left == False:
                    faller.shift_left()
                    for i in range(self.rows()):
                        if self._field[i][faller.column_to_drop() + 1].state() == 'faller' or self._field[i][faller.column_to_drop() + 1].state() == 'landed':
                            temp = self._field[i][faller.column_to_drop() + 1].contents()
                            self._field[i][faller.column_to_drop()].update(temp)
                            self._field[i][faller.column_to_drop() + 1].update(' ')
                    for j in range(self.rows() - 1):
                        if self._field[j][faller.column_to_drop()].state() == 'landed' and self._field[j + 1][faller.column_to_drop()].state() == 'empty':
                            for k in range(j + 1):
                                if self._field[k][faller.column_to_drop()].state() == 'landed':
                                    self._field[k][faller.column_to_drop()].change_to_faller()
                        if self._field[j][faller.column_to_drop()].state() == 'faller' and self._field[j + 1][faller.column_to_drop()].state() == 'frozen':
                            for k in range(j + 1):
                                if self._field[k][faller.column_to_drop()].state() == 'faller':
                                    self._field[k][faller.column_to_drop()].landed()
            else:
                pass
        else:
            pass