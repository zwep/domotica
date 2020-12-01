program readfromfile
    integer, dimension(200,1) :: cs

    open(unit=15, file='./adventofcode_2020/day1_numbers.txt', status='old', action='read')
    read(15,*) cs
    do i=1,200
        print *, cs(i, 1)
    end do

end program readfromfile